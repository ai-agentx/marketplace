<template>
  <div class="flex justify-center items-center" :class="heightClass">
    <div class="relative">
      <div class="animate-spin rounded-full" 
           :class="[
             `h-${size} w-${size}`, 
             `border-${borderWidth}`, 
             `border-${color}`, 
             `border-t-transparent`
           ]">
      </div>
      <div v-if="showText" class="mt-2 text-center text-gray-600">
        {{ text }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    size: {
      type: String,
      default: '8'
    },
    color: {
      type: String,
      default: 'indigo-500'
    },
    borderWidth: {
      type: String,
      default: '4'
    },
    text: {
      type: String,
      default: 'Loading...'
    },
    showText: {
      type: Boolean,
      default: true
    },
    height: {
      type: String,
      default: '64' // h-64
    }
  },
  computed: {
    heightClass() {
      return `h-${this.height}`
    }
  }
}
</script>
