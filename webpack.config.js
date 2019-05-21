const path = require('path');
const webpack = require('webpack');

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
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [['@babel/preset-env', { modules: false }]]      //Modules false -> no require() convertion
          }
        }
      }
    ]
  }
}