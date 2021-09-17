// const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')

module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  configureWebpack: {
    plugins: [
      // new VuetifyLoaderPlugin(),
      // new UglifyJsPlugin(),
      // new OptimizeCSSPlugin(),
    ],
    resolve: {
      alias: {
      
      },
      extensions: ['.js', '.vue', '.json']
    }
  }
}
