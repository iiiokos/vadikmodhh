package com.example.vadikmod;

import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.resources.ResourceLocation;

public class VadikRenderer extends HumanoidMobRenderer<VadikEntity, VadikModel> {

    private static final ResourceLocation TEXTURE =
            ResourceLocation.fromNamespaceAndPath(VadikMod.MOD_ID, "textures/entity/vadik.png");

    public VadikRenderer(EntityRendererProvider.Context context) {
        super(context, new VadikModel(context.bakeLayer(VadikModel.LAYER_LOCATION)), 0.5F);
    }

    @Override
    public ResourceLocation getTextureLocation(VadikEntity entity) {
        return TEXTURE;
    }
}
