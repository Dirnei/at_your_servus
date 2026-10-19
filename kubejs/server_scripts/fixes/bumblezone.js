// The Bumblezone 7.18.0: the Potion Candle recipes break on the network (ShapedRecipePattern with no rows), and a
// client joining a world that syncs crafting recipes is disconnected. Remove them until Bumblezone fixes it (docs/gates.md).
ServerEvents.recipes(event => {
  event.remove({ type: 'the_bumblezone:potion_candle_recipe' })
})
