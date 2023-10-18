<script lang="ts">
  import { onMount } from "svelte";
  import Value from "./lib/Value.svelte";

  let data: ClimatePoint[] = [];
  $: last = data[data.length - 1];

  onMount(async () => {
    const req = await fetch("http://pc.lego:5000/api/data");
    const body = await req.json();

    data = body.data;
  });
</script>

<div class="container mx-auto my-2">
  <h1 class="text-3xl font-semibold">Hello World</h1>

  {#if last}
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
        min={0}
        max={100}
      />
    </div>
  {/if}

  <pre>{JSON.stringify(data, null, 2)}</pre>
</div>
