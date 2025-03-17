module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:9091',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      }
    }
  }
}
