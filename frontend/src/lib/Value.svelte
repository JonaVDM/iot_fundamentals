<script lang="ts">
  import { Gauge, Donut } from "gaugeJS/dist/gauge";

  export let value: number;
  export let min: number;
  export let max: number;
  export let label: string;
  export let symbol: string;

  function canvasAction(container: HTMLCanvasElement) {
    var opts = {
      angle: 0,
      lineWidth: 0.3,
      radiusScale: 1,
      pointer: {
        length: 0,
        strokeWidth: 0,
      },
      limitMax: false,
      limitMin: false,
      colorStart: "#6FADCF",
      colorStop: "#8FC0DA",
      strokeColor: "#E0E0E0",
      generateGradient: true,
      highDpiSupport: true,
    };
    var gauge = new Gauge(container).setOptions(opts);
    gauge.maxValue = max;
    gauge.setMinValue(min);
    gauge.animationSpeed = 60;
    gauge.set(value);
  }
</script>

<div class="w-full text-center">
  <canvas class="mx-auto" use:canvasAction />
  <p class="font-semibold text-xl">{value}{symbol}</p>
  <p class="font-light text-sm">{label}</p>
</div>
