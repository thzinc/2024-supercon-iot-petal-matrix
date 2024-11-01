const LOCAL_STORAGE_KEY_DEVICE_ID = "device-id";
const REQUEST_TYPE_TOUCH = 1;

const decoder = new TextDecoder();

function buildTopic(relativePath) {
  const prefix = "thzinc/2024-supercon";
  const deviceId = localStorage.getItem(LOCAL_STORAGE_KEY_DEVICE_ID);

  return `${prefix}/${(deviceId || "").replace(
    /[^a-z\d\-_]+/gi,
    ""
  )}/${relativePath}`;
}

window.addEventListener("load", () => {
  const mqttStatusEl = document.getElementById("mqtt-status");
  const deviceIdEl = document.getElementById("device-id");
  const deviceStatusEl = document.getElementById("device-status");
  const svg = document.getElementById("petal-matrix").contentDocument;

  const client = mqtt.connect("wss://broker.emqx.io:8084/mqtt");
  client.on("connect", () => {
    mqttStatusEl.textContent = "Connected";
  });
  client.on("reconnect", () => {
    mqttStatusEl.textContent = "Reconnected";
  });
  client.on("disconnect", () => {
    mqttStatusEl.textContent = "Disconnected";
  });
  client.on("offline", () => {
    mqttStatusEl.textContent = "Offline";
  });
  client.on("error", () => {
    mqttStatusEl.textContent = "Error";
  });
  client.on("message", (topic, message, packet) => {
    console.debug({ topic, message, packet });
    if (topic.endsWith("/leds/spiral/row")) {
      const [row, cols] = Array.from(message);
      console.debug({ row, cols });
      for (let col = 0; col < 7; col++) {
        const id = `led-${row}-${col + 1}`;
        const el = svg.getElementById(id);
        if (el) {
          if (cols & (1 << col)) {
            el.classList.add("active");
          } else {
            el.classList.remove("active");
          }
        } else {
          console.debug("Failed to find element", id);
        }
      }
    }
  });

  let isDown = false;
  let lastTarget = null;
  const startDrawing = (ev) => {
    if (!enabled) return;
    isDown = true;
    handleMove(ev);
  };
  svg.addEventListener("pointerdown", startDrawing);
  svg.addEventListener("touchstart", startDrawing);

  const stopDrawing = () => {
    if (!enabled) return;
    isDown = false;
    lastTarget = null;
  };
  svg.addEventListener("pointerup", stopDrawing);
  svg.addEventListener("touchend", stopDrawing);
  svg.addEventListener("pointercancel", stopDrawing);
  svg.addEventListener("touchcancel", stopDrawing);

  const handleMove = ({ pageX, pageY }) => {
    if (!enabled) return;
    if (!isDown) return;

    const target = svg.elementFromPoint(pageX, pageY);
    if (!target) return;
    if (target === lastTarget) return;
    lastTarget = target;

    const row = target.dataset.row;
    const col = target.dataset.col;
    client.publish(
      buildTopic("requests"),
      decoder.decode(new Uint8Array([REQUEST_TYPE_TOUCH, row, col]))
    );
  };
  svg.addEventListener("pointermove", (ev) => {
    ev.preventDefault();
    if (!enabled) return;
    handleMove(ev);
  });
  svg.addEventListener("touchmove", (ev) => {
    ev.preventDefault();
    if (!enabled) return;
    if (ev.touches.length === 0) return;
    handleMove(ev.touches[0]);
  });

  let enabled = false;
  function enable() {
    enabled = true;

    deviceIdEl.textContent = localStorage.getItem(LOCAL_STORAGE_KEY_DEVICE_ID);
    deviceStatusEl.textContent = "Enabled";

    client.subscribe(buildTopic("leds/spiral/row"));
  }

  function disable() {
    enabled = false;

    deviceIdEl.textContent =
      localStorage.getItem(LOCAL_STORAGE_KEY_DEVICE_ID) || "Unknown";
    deviceStatusEl.textContent = "Disabled";

    client.unsubscribe(buildTopic("leds/spiral/row"));
  }

  function tryEnable() {
    const deviceId = localStorage.getItem(LOCAL_STORAGE_KEY_DEVICE_ID);
    if (deviceId && deviceId !== "") {
      return enable();
    }

    return disable();
  }

  tryEnable();

  deviceIdEl.addEventListener("click", () => {
    const deviceId = prompt(
      "Enter your device's configured ID",
      localStorage.getItem(LOCAL_STORAGE_KEY_DEVICE_ID) || ""
    );

    if (deviceId === null) return;
    disable();

    localStorage.setItem(
      LOCAL_STORAGE_KEY_DEVICE_ID,
      deviceId.replace(/[^a-z\d\-_]+/gi, "")
    );
    tryEnable();
  });
});
