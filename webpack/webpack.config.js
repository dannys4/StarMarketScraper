const path = require("path");
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
   mode: "development",
   entry: {
      background: path.resolve(__dirname, "..", "src", "background.ts"),
      // add other entries like content scripts here
   },
   output: {
      path: path.join(__dirname, "..", "dist"),
      filename: "[name].js",
      clean: true
   },
   resolve: {
      extensions: [".ts", ".js", ".png"]
   },
   module: {
      rules: [
         {
            test: /\.tsx?$/,
            loader: "ts-loader",
            exclude: /node_modules/,
         },
      ],
   },
   target: "webworker",
   devtool: "source-map",
   plugins: [
      new CopyPlugin({
         patterns: [{ from: ".", to: ".", context: "public" }, { from: ".", to: ".", context: "images" }]
      }),
   ],
};
