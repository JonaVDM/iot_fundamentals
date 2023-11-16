<script lang="ts">
  import { onMount } from "svelte";
  import Value from "./lib/Value.svelte";
  import Graph from "./lib/Graph.svelte";
  import Prediction from "./lib/Prediction.svelte";

  let data: ClimatePoint[] = [];
  let last: ClimatePoint | null = null;
  $: labels = data.map((d) => new Date(d.time).toLocaleTimeString()); // const labels =
  $: date = last ? new Date(last.time) : "";

  let start: string;
  let end: string;

  onMount(async () => {
    const req = await fetch("/api/data");
    const body = await req.json();

    data = body.data.reverse();
    last = data[data.length - 1];
  });

  async function load() {
    let s = new Date(start);
    let e = new Date(end);

    const req = await fetch(
      `/api/data?start=${formatTime(s)}&end=${formatTime(e)}`
    );
    const body = await req.json();
    data = body.data.reverse();
  }

  function formatTime(time: Date) {
    let year = time.getUTCFullYear();
    let month = padLeft(time.getUTCMonth() + 1);
    let day = padLeft(time.getUTCDate());
    let hour = padLeft(time.getUTCHours());
    let minute = padLeft(time.getUTCMinutes());
    let second = padLeft(time.getUTCSeconds());
    return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
  }

  function padLeft(num: number) {
    return ("0" + num).slice(-2);
  }
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

  <div class="grid grid-cols-2 gap-2 max-w-lg text-black mx-auto py-4">
    <input type="datetime-local" bind:value={start} />
    <input type="datetime-local" bind:value={end} />
    <button
      class="col-span-2 bg-green-600 text-gray-200 py-2 rounded-md"
      on:click={load}
    >
      Load
    </button>
  </div>

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
