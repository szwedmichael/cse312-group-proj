module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  plugins: [require("daisyui")],
  // corePlugins: {
  //   preflight: false,
  // },
  daisyui: {
    darkTheme: "light",
    base:false,
   },

}
