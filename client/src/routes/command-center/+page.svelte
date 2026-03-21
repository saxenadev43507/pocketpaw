<!-- Redirect /command-center to /pockets (renamed in v0.4.11) -->
<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  onMount(() => goto("/pockets", { replaceState: true }));
</script>
