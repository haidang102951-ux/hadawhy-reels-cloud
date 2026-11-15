import React from "react";
import { HaDaWhyUniversal9x16, UniversalScenePlan } from "./HaDaWhyUniversal9x16";
import defaultPlan from "./scene_plan.json";

export const DynamicReel: React.FC<{ plan?: UniversalScenePlan }> = ({
  plan = defaultPlan as unknown as UniversalScenePlan,
}) => {
  return <HaDaWhyUniversal9x16 plan={plan} />;
};
