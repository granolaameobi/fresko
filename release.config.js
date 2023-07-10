const fs = require('fs');

module.exports = {
  branches: ['main'],
  plugins: [
    [
        "@semantic-release/commit-analyzer",
        {
          "preset": "angular"
        }
    ],
    '@semantic-release/release-notes-generator',
    '@semantic-release/github',
    [
      '@semantic-release/exec',
      {
        prepareCmd: 'echo "${nextRelease.version}" > version.txt',
      },
    ],
    '@semantic-release/git'
  ],
  // Write the version to a file after the release
  success: function (pluginConfig, { nextRelease }) {
    fs.writeFileSync('./version.txt', nextRelease.version, { encoding: 'utf-8' });
  },
};
