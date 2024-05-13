<script lang="ts">
  import TattooPhotoViewer from './tattoo-photo-viewer.svelte';
  import TattooVideoViewer from './tattoo-video-viewer.svelte';

  export let tattooFilePath: string = '';
  export let mediaMode: string = '';
  export let assetId: string = '';

  const handleVideoStarted = () => {
  };

  const handleVideoEnded = async () => {
  };

</script>

<div class="flex gap-4">
  <div class="h-full w-full shrink-0 bg-slate-300">
    {#if mediaMode === 'image'}
      <TattooPhotoViewer filePath={tattooFilePath} />
    {:else}
      <TattooVideoViewer assetId={assetId} filePath={tattooFilePath} on:onVideoEnded={handleVideoEnded} on:onVideoStarted={handleVideoStarted}/>
  {/if}
  </div>
</div>