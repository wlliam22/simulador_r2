"use strict";

const fs = require("fs");
const path = require("path");

const htmlPath = path.join(__dirname, "..", "web", "index.html");
const html = fs.readFileSync(htmlPath, "utf8");
const functionMatch = html.match(
  /function calculate\(speed, degrees\) \{[\s\S]*?\n      \}/
);

if (!functionMatch) {
  throw new Error("No se encontró la función calculate en index.html");
}

const calculate = new Function(
  "gravity",
  "target",
  `${functionMatch[0]}; return calculate;`
)(9.81, { left: 85, width: 12, height: 8 });

const cases = [
  { name: "techo", speed: 32, angle: 53, type: "structure", x: 93.9 },
  { name: "lado", speed: 40, angle: 20, type: "structure", x: 85 },
  { name: "pasa", speed: 45, angle: 45, type: "ground", x: 206.42 },
  { name: "antes", speed: 20, angle: 45, type: "ground", x: 40.77 }
];

let failures = 0;

for (const testCase of cases) {
  const result = calculate(testCase.speed, testCase.angle);
  const xMatches = Math.abs(result.impactX - testCase.x) < 0.1;
  const passed = result.impactType === testCase.type && xMatches;

  console.log(
    `${passed ? "PASS" : "FAIL"} ${testCase.name}: ${result.impactType}, ` +
      `x=${result.impactX.toFixed(2)} m, y=${result.impactY.toFixed(2)} m, ` +
      `t=${result.impactTime.toFixed(2)} s`
  );

  if (!passed) failures += 1;
}

if (failures > 0) {
  process.exit(1);
}
