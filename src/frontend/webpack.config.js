const path = require('path');


module.exports = {
  mode: 'development',
  entry: {
    index: './src/index.tsx',
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
      api: path.resolve(__dirname, './src/api/'),
      'velvet-dawn': path.resolve(__dirname, './src/velvet-dawn/'),
      models: path.resolve(__dirname, './src/models/'),
      ui: path.resolve(__dirname, './src/ui/'),
      rendering: path.resolve(__dirname, './src/rendering/'),
      entity: path.resolve(__dirname, './src/entity/'),
    }
  },
  output: {
    filename: 'app.js',
    path: path.resolve(__dirname, 'dist'),
  },
  devServer: {
    static: "./dist",
    historyApiFallback: true
  }
};