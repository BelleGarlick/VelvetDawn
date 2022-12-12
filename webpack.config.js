const path = require('path');


module.exports = {
  mode: 'development',
  entry: {
    index: './fe/index.tsx',
    // worker: './src/compute-worker.ts',
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      }
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
    alias: {
      api: path.resolve(__dirname, './fe/api/'),
      models: path.resolve(__dirname, './fe/models/'),
      ui: path.resolve(__dirname, './fe/ui/'),
    }
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  devServer: {
    static: "./dist",
    historyApiFallback: true
  }
};