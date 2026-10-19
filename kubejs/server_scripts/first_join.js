// Gives every player the FTB Quests book once, on their first join. The stage is saved with the player.
PlayerEvents.loggedIn(event => {
  const player = event.player
  if (player.stages.has('servus_got_quest_book')) return
  player.give('ftbquests:book')
  player.stages.add('servus_got_quest_book')
})
