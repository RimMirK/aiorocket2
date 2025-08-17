// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'aiorocket2',
  tagline: 'asynchronous Python client for the xRocket Pay API',
  favicon: 'img/aiorocket_logo.png',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://aiorocket2.rimmirk.pp.ua',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'RimMirK', // Usually your GitHub org/user name.
  projectName: 'aiorocket2', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/RimMirK/aiorocket2/blob/main/docs-website/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/aiorocket_logo.png',
      navbar: {
        title: 'aiorocket2',
        logo: {
          alt: 'aiorocket2',
          src: 'img/aiorocket_logo.png',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialsSidebar',
            position: 'left',
            label: 'Tutorials',
          },
          {
            type: 'docSidebar',
            sidebarId: 'api_referenceSidebar',
            position: 'left',
            label: 'API Reference',
          },
          {
            href: 'https://github.com/RimMirK/aiorocket2',
            label: 'GitHub',
            position: 'right',
          },{
            href: 'https://pypi.org/project/aiorocket2',
            label: 'PyPI',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Navigation',
            items: [
              {
                label: 'Tutorials',
                to: '/docs/tutorials',
              },
              {
                label: 'API Reference',
                to: '/docs/api-reference',
              }
            ],
          },
          {
            title: 'Links',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/RimMirK/aiorocket2',
              },
              {
                label: 'PyPI',
                href: 'https://pypi.org/project/aiorocket2',
              },
              {
                label: 'Telegram (developer)',
                href: 'https://t.me/RimMirK?text=Hi!+I+am+writing+to+you+regarding+aiorocket2',
              },
            ],
          },
          {
            title: 'Donate',
            items: [
              {
                label: 'xRocket',
                href: 'https://t.me/xrocket?start=inv_ay2rHoUo5O5aNGS',
              },
              {
                label: 'CryptoBot',
                href: 'https://t.me/send?start=IVj8IjduvvAN',
              },
              {
                label: 'Other',
                href: 'https://t.me/RimMirK?text=Hi!+I+want+to+donate+to+u+because+I+love+aiorocket2',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} RimMirK. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
