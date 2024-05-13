<script lang="ts">
  import {api } from '@api';
  import { createEventDispatcher, onMount } from 'svelte';
  import BaseModal from './base-modal.svelte';
  import TattoosListItem from '../asset-viewer/tattoos-list-item.svelte';
  import { handleError } from '$lib/utils/handle-error';

  let tattooFilePath: string = '';
  let mediaMode: string = '';
  let loading = true;
  export let assetId: string = '';

  const dispatch = createEventDispatcher<{
    close: void;
  }>();

  onMount(async () => {
    
    try {
      const { data } = await api.tattoosRecognizeApi.getTattoosRecognize({ id: assetId });
      tattooFilePath = data.filePath;
      mediaMode = data.mediaMode;
    } catch (error) {
    handleError(error, "Internal Server Error! Cannot Detect Tattoos.");
  }

    loading = false;
  });

</script>

<BaseModal on:close={() => dispatch('close')}>
  <svelte:fragment slot="title">
    <span class="flex place-items-center gap-2">
      <p class="font-medium">
        {#if loading}
          Detecting...
        {:else if tattooFilePath !== ''}
          Tattoo Detected!
        {:else}
          No Tattoo Detected!
        {/if}
      </p>
    </span>
  </svelte:fragment>

  <div class="mb-2 flex max-h-[90vh] flex-col">
    {#if loading}
      {#each { length: 3 } as _}
        <div class="flex animate-pulse gap-4 px-6 py-2">
          <div class="h-12 w-12 rounded-xl bg-slate-200" />
          <div class="flex flex-col items-start justify-center gap-2">
            <span class="h-4 w-36 animate-pulse bg-slate-200" />
            <div class="flex animate-pulse gap-1">
              <span class="h-3 w-8 bg-slate-200" />
              <span class="h-3 w-20 bg-slate-200" />
            </div>
          </div>
        </div>
      {/each}
    {:else}
      <!-- svelte-ignore a11y-autofocus -->
      <div class="immich-scrollbar overflow-y-auto">
        {#if tattooFilePath !== ''}
          <div class="flex gap-4 px-6 py-2">
            <div class="h-full w-full shrink-0 bg-slate-300">
          <!-- {#each weapons as weapon (weapon.image)} -->
              <TattoosListItem assetId={assetId} tattooFilePath={tattooFilePath} mediaMode={mediaMode} />
          <!-- {/each} -->
            </div>
          </div>
        <!-- {:else}
          <p class="px-5 py-1 text-sm">No Weapons Detected!</p> -->
        {/if}
      </div>
    {/if}
  </div>
</BaseModal>
