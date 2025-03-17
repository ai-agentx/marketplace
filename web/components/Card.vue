<template>
  <div 
    class="bg-white shadow rounded-lg overflow-hidden"
    :class="{ 'hover:shadow-md transition-shadow': hover }"
  >
    <div v-if="$slots.header" class="p-6 border-b">
      <slot name="header"></slot>
    </div>
    <div class="p-6">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="p-6 border-t bg-gray-50">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    hover: {
      type: Boolean,
      default: false
    }
  }
}
</script>
