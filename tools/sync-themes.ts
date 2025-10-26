/**
 * Sync Bulma and Bulmaswatch versions into themes.
 */
import bulma from "bulma/package.json";
import bulmaswatch from "bulmaswatch/package.json";

console.log(`Bulma version:       ${bulma.version}`);
console.log(`Bulmaswatch version: ${bulmaswatch.version}`);

const targets = ["src/atsphinx/bulma/themes/bulma_basic/theme.toml"];

targets.forEach(async (target) => {
  let theme = await Bun.file(target).text();
  theme = theme.replace(
    /bulma_version = ".*"/,
    `bulma_version = "${bulma.version}"`,
  );
  theme = theme.replace(
    /bulmaswatch_version = ".*"/,
    `bulmaswatch_version = "${bulmaswatch.version}"`,
  );
  await Bun.write(target, theme);
});
