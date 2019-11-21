#! /usr/bin/env node
// @ts-check
const fetch = require("node-fetch");
const { writeFileSync } = require("fs");
const { isDir } = require('path');

/**
 *
 * @param {number} amt
 */
const sleep = amt =>
  new Promise(resolve => {
    setTimeout(() => {
      resolve();
    }, amt);
  });

let allCards = [];

/**
 *
 * @param {string} queryString
 */
async function getAllCardsJson(queryString) {
  console.log("fetching page from api");
  let response = await fetch(
    `https://api.scryfall.com/cards/search?q=${encodeURIComponent(queryString)}`
  ).then(r => r.json());
  allCards = allCards.concat(response.data);

  while (response.next_page) {
    console.log(`fetching next from api (${allCards.length} cards so far)`);
    await sleep(100);
    response = await fetch(response.next_page).then(r => r.json());
    allCards = allCards.concat(response.data);
  }

  return allCards;
}

async function main() {
  const queryString = process.argv.slice(2).join(" ");
  if (queryString == "") {
    console.log(`Usage: ${process.argv0} <scryfall query string>`);
    process.exit(0);
  }

  const allowedChars = new Set(
    "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm:1234567890".split("")
  );

  const escapedQuery = queryString
    .split("")
    .map(x => (allowedChars.has(x) ? x : "-"))
    .join("");
  const outFileName = `./data/${escapedQuery}.json`;

  const cards = await getAllCardsJson(queryString);
  for(let card of cards) {
    if(not)
  } 
}

main();
