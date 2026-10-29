package com.example.vadikmod;

import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;

/**
 * Гуманоидная модель Вадика с дополнительными 3D-деталями:
 * длинные волосы, чёлка, очки, наушник, браслет и карманы шорт.
 * Раскладка текстуры: 64x64, как у скина игрока; доп. детали лежат
 * в свободных областях (см. make_skin.py).
 */
public class VadikModel extends HumanoidModel<VadikEntity> {

    public static final ModelLayerLocation LAYER_LOCATION = new ModelLayerLocation(
            ResourceLocation.fromNamespaceAndPath(VadikMod.MOD_ID, "vadik"), "main");

    public VadikModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition root = mesh.getRoot();

        // ---------- голова ----------
        PartDefinition head = root.getChild("head");

        // длинные волосы сзади и по бокам (до плеч)
        head.addOrReplaceChild("hair_back",
                CubeListBuilder.create().texOffs(0, 32)
                        .addBox(-4.0F, -8.0F, 4.0F, 8.0F, 10.0F, 2.0F, new CubeDeformation(0.25F)),
                PartPose.ZERO);
        head.addOrReplaceChild("hair_side_r",
                CubeListBuilder.create().texOffs(20, 32)
                        .addBox(-5.0F, -8.0F, -1.0F, 1.0F, 10.0F, 5.0F),
                PartPose.ZERO);
        head.addOrReplaceChild("hair_side_l",
                CubeListBuilder.create().texOffs(32, 32)
                        .addBox(4.0F, -8.0F, -1.0F, 1.0F, 10.0F, 5.0F),
                PartPose.ZERO);
        // чёлка
        head.addOrReplaceChild("fringe",
                CubeListBuilder.create().texOffs(44, 32)
                        .addBox(-4.0F, -8.25F, -4.75F, 8.0F, 2.0F, 1.0F),
                PartPose.ZERO);

        // очки: две линзы, переносица, дужки
        head.addOrReplaceChild("lens_r",
                CubeListBuilder.create().texOffs(44, 36)
                        .addBox(-3.5F, -5.5F, -5.0F, 3.0F, 3.0F, 1.0F),
                PartPose.ZERO);
        head.addOrReplaceChild("lens_l",
                CubeListBuilder.create().texOffs(44, 36)
                        .addBox(0.5F, -5.5F, -5.0F, 3.0F, 3.0F, 1.0F),
                PartPose.ZERO);
        head.addOrReplaceChild("bridge",
                CubeListBuilder.create().texOffs(52, 36)
                        .addBox(-0.5F, -4.5F, -5.0F, 1.0F, 1.0F, 1.0F),
                PartPose.ZERO);
        head.addOrReplaceChild("temple_r",
                CubeListBuilder.create().texOffs(44, 40)
                        .addBox(-5.0F, -4.5F, -5.0F, 1.0F, 1.0F, 5.0F, new CubeDeformation(-0.25F)),
                PartPose.ZERO);
        head.addOrReplaceChild("temple_l",
                CubeListBuilder.create().texOffs(44, 40)
                        .addBox(4.0F, -4.5F, -5.0F, 1.0F, 1.0F, 5.0F, new CubeDeformation(-0.25F)),
                PartPose.ZERO);

        // беспроводной наушник в правом ухе
        head.addOrReplaceChild("earbud",
                CubeListBuilder.create().texOffs(56, 36)
                        .addBox(-5.2F, -4.5F, -2.0F, 1.0F, 2.0F, 1.0F),
                PartPose.ZERO);

        // ---------- правая рука: браслет на запястье ----------
        PartDefinition rightArm = root.getChild("right_arm");
        rightArm.addOrReplaceChild("wristband",
                CubeListBuilder.create().texOffs(0, 48)
                        .addBox(-3.0F, 7.0F, -2.0F, 4.0F, 1.0F, 4.0F, new CubeDeformation(0.3F)),
                PartPose.ZERO);

        // ---------- ноги: карманы карго-шорт ----------
        PartDefinition rightLeg = root.getChild("right_leg");
        rightLeg.addOrReplaceChild("pocket_r",
                CubeListBuilder.create().texOffs(0, 56)
                        .addBox(-3.0F, 2.0F, -1.5F, 1.0F, 3.0F, 3.0F),
                PartPose.ZERO);
        PartDefinition leftLeg = root.getChild("left_leg");
        leftLeg.addOrReplaceChild("pocket_l",
                CubeListBuilder.create().texOffs(0, 56)
                        .addBox(2.0F, 2.0F, -1.5F, 1.0F, 3.0F, 3.0F),
                PartPose.ZERO);

        return LayerDefinition.create(mesh, 64, 64);
    }

    @Override
    public void setupAnim(VadikEntity entity, float limbSwing, float limbSwingAmount,
                          float ageInTicks, float netHeadYaw, float headPitch) {
        super.setupAnim(entity, limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch);

        // держит книжку перед собой и чуть "дышит"
        if (!entity.getMainHandItem().isEmpty()) {
            this.rightArm.xRot = -0.95F + Mth.cos(ageInTicks * 0.09F) * 0.03F - limbSwingAmount * 0.2F;
            this.rightArm.yRot = -0.15F;
            this.rightArm.zRot = 0.0F;
        }
    }
}
