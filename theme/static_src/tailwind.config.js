

module.exports = {

    content: [

        '../templates/**/*.html',
        '../static/**/*.js',
        '../static/**/*.css',

        '../../templates/**/*.html',

        '../../**/templates/**/*.html',

    ],
    theme: {
        extend: {
          colors: {
            "custom-main": "#ff5733",
            "highlight-bg": "#f4f4f4",
            "action-color": "#34d399",
            "created-blue": "#128aff",
            "created-orange": "#e65c0b",
            "created-pink":"#c4009b",
          },
          screens: {
            l: '360px',
            sm: '640px',
            md: '768px',
            lg: '992px',
            xl: '1280px',
            xxl: '1440px',
          },
        },
      },

      daisyui: {
        themes: [
          {
            light: {
              "primary": "#000000",
              "secondary": "#ffffff",
              "accent": "#22c55e",
              "neutral": "#f3f4f6",
              "base-100": "#ffffff",
            },
          },
          {
            dark: {
              "primary": "#ffffff",
              "secondary": "#000000",
              "accent": "#22c55e",
              "neutral": "#1f2937",
              "base-100": "#111827",
            },
          },
        ],
      },

    plugins: [

        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('daisyui'),
    ],
}
