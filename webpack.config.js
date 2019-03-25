const path = require('path');

module.exports = {
  entry: {
    app: './static/js/main.js'
  },
  output: {
    path: path.resolve(__dirname, 'static', 'js'),
    filename: '[name].bundle.js',
    libraryTarget: 'var',
    library: 'TE'
  },
  module: {
    rules: [
      {
        test: /\.hbs$/,
        exclude: /node_modules/,
        use: {
          loader: 'handlebars-loader'
        }
      }
    ]
  }
}