<script lang="ts">
  export let value: number;
  export let min: number;
  export let max: number;
  export let label: string;
  export let symbol: string;
</script>

<div class="w-full text-center">
  <p class="font-semibold text-xl">{value}{symbol}</p>
  <p class="font-light text-sm">{label}</p>
</div>
