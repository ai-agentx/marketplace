<template>
  <span 
    :class="`px-2 py-1 text-xs rounded-full ${getColorClasses}`"
  >
    <slot></slot>
  </span>
</template>

<script>
export default {
  name: 'Badge',
  props: {
    color: {
      type: String,
      default: 'indigo',
      validator: (value) => ['indigo', 'green', 'red', 'yellow', 'blue', 'gray'].includes(value)
    },
    variant: {
      type: String,
      default: 'light',
      validator: (value) => ['light', 'solid'].includes(value)
    }
  },
  computed: {
    getColorClasses() {
      const colorMap = {
        indigo: {
          light: 'bg-indigo-100 text-indigo-800',
          solid: 'bg-indigo-600 text-white'
        },
        green: {
          light: 'bg-green-100 text-green-800',
          solid: 'bg-green-600 text-white'
        },
        red: {
          light: 'bg-red-100 text-red-800',
          solid: 'bg-red-600 text-white'
        },
        yellow: {
          light: 'bg-yellow-100 text-yellow-800',
          solid: 'bg-yellow-600 text-white'
        },
        blue: {
          light: 'bg-blue-100 text-blue-800',
          solid: 'bg-blue-600 text-white'
        },
        gray: {
          light: 'bg-gray-100 text-gray-800',
          solid: 'bg-gray-600 text-white'
        }
      }
      
      return colorMap[this.color][this.variant]
    }
  }
}
</script>
