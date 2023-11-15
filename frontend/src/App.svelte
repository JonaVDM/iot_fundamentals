<script lang="ts">
  import { onMount } from "svelte";
  import Value from "./lib/Value.svelte";
  import Graph from "./lib/Graph.svelte";
  import Prediction from "./lib/Prediction.svelte";

  let data: ClimatePoint[] = [];
  $: last = data[0];
  $: labels = data.map((d) => new Date(d.time).toLocaleTimeString()); // const labels =
  $: date = new Date(last?.time);

  onMount(async () => {
    const req = await fetch("http://pc.lego:5000/api/data");
    const body = await req.json();

    data = body.data.reverse();
  });
</script>

<div class="container mx-auto my-2">
  {#if last}
    <p class="text-sm font-extralight italic">
      Last measurement at {date.toLocaleString()}
    </p>

    <div class="flex gap-2 justify-between">
      <Value
        label="temperature"
        symbol="°C"
        value={last.temperature}
        min={-10}
        max={50}
      />

      <Value
        label="Humidity"
        symbol="%"
        value={last.humidity}
        min={0}
        max={100}
      />

      <Value
        label="Pressure"
        symbol="hPa"
        value={last.pressure}
        min={800}
        max={1200}
      />
    </div>
  {/if}

  {#key data}
    <div class="flex flex-col gap-4">
      <Graph
        data={data.map((d) => d.temperature)}
        {labels}
        label="Temperature"
      />
      <Graph data={data.map((d) => d.humidity)} {labels} label="Humidity" />
      <Graph data={data.map((d) => d.pressure)} {labels} label="Pressure" />
    </div>
  {/key}

  <Prediction />
</div>
