<script lang="ts">
  import { onMount } from "svelte";

  let data: ClimatePoint[] = [];

  onMount(async () => {
    const req = await fetch("http://pc.lego:5000/api/data");
    const body = await req.json();

    data = body.data;
  });
</script>

<h1 class="text-3xl font-semibold">Hello World</h1>
