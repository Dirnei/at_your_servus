// Re:Avaritia: the Infinity Catalyst needs the Rubedo products of Servus: Alchemy, the trading house's Crafting CPU
// and the power station's top crystal, so the capstone comes after the Great Work (docs/gates.md).
const SERVUS_CATALYST_PARTS = [
  'servus_alchemy:ignis_perpetuus',
  'servus_alchemy:quicksilver',
  'servus_alchemy:caput_mortuum',
  'servus_shuttles:crafting_cpu',
  'powah:crystal_nitro'
]

ServerEvents.recipes(event => {
  const base = ['minecraft:bedrock', 'avaritia:crystal_matrix_ingot', 'avaritia:neutron_ingot', 'avaritia:cosmic_meatballs',
    'avaritia:ultimate_stew', 'avaritia:endest_pearl', 'avaritia:record_fragment']

  event.remove({ id: 'avaritia:infinity_catalyst' })
  event.custom({ type: 'avaritia:infinity_catalyst', ingredients: base.concat(SERVUS_CATALYST_PARTS) })
    .id('servus:gates/infinity_catalyst')

  event.remove({ id: 'avaritia:infinity_catalyst_eternal' })
  event.custom({
    type: 'avaritia:infinity_catalyst',
    group: 'eternal_singularity',
    ingredients: base.concat(['avaritia:eternal_singularity'], SERVUS_CATALYST_PARTS)
  }).id('servus:gates/infinity_catalyst_eternal')
})
