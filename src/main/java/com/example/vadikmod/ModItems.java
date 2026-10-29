package com.example.vadikmod;

import net.minecraft.world.item.Item;
import net.minecraftforge.common.ForgeSpawnEggItem;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public class ModItems {
    public static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(ForgeRegistries.ITEMS, VadikMod.MOD_ID);

    // тёмно-синий (футболка) + цвет кожи
    public static final RegistryObject<Item> VADIK_SPAWN_EGG = ITEMS.register("vadik_spawn_egg",
            () -> new ForgeSpawnEggItem(ModEntities.VADIK, 0x1B1E2D, 0xE6BEA0, new Item.Properties()));
}
