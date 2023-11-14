<script lang="ts">
  import { Chart } from "chart.js/auto";

  export let labels: string[];
  export let data: number[];
  export let label: string;

  function chartAction(container: HTMLCanvasElement) {
    const ctx = container.getContext("2d");
    if (!ctx) {
      return;
    }

    new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            data,
            label,
          },
        ],
      },
      options: {
        responsive: false,
        maintainAspectRatio: false,
      },
    });
  }
</script>

<canvas style="height:350px;" use:chartAction />
