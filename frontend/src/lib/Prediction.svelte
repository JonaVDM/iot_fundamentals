<script lang="ts">
  import { onMount } from "svelte";
  let prediction = "";

  onMount(async () => {
    const req = await fetch("http://localhost:5000/api/prediction");
    const data = await req.json();

    if (data.predicion == 1) {
      prediction = "Its probably not going to rain";
    } else {
      prediction = "There is a very good change it is going to rain";
    }
  });
</script>

<div>
  <h2 class="text-xl font-light">What does the AI say?</h2>
  <p>{prediction}</p>
</div>
