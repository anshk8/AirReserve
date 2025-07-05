const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');
require('dotenv').config();

module.exports = {
  mode: 'development',
  entry: './src/ui/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    publicPath: '/'
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/ui/public/index.html',
      filename: 'index.html'
    }),
    new webpack.DefinePlugin({
      'process.env.REACT_APP_FIREBASE_PROJECT_ID': JSON.stringify(process.env.REACT_APP_PROJECT_ID || process.env.FIREBASE_PROJECT_ID),
      'process.env.REACT_APP_FIREBASE_DATABASE_URL': JSON.stringify(process.env.REACT_APP_DATABASE_URL || process.env.FIREBASE_DATABASE_URL),
      'process.env.FIREBASE_PROJECT_ID': JSON.stringify(process.env.FIREBASE_PROJECT_ID),
      'process.env.FIREBASE_DATABASE_URL': JSON.stringify(process.env.FIREBASE_DATABASE_URL)
    })
  ],
  devServer: {
    static: {
      directory: path.join(__dirname, 'src/ui/public'),
    },
    compress: true,
    port: 3000,
    historyApiFallback: true,
    hot: true
  }
};
