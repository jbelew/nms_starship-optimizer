import React from "react";
import { useGridStore } from "../store/useGridStore";
import { useTechStore } from "../store/useTechStore";
import { IconButton, Flex, Text, Tooltip } from "@radix-ui/themes";
import { UpdateIcon, ResetIcon, DoubleArrowLeftIcon } from "@radix-ui/react-icons";

interface OptimizationButtonProps {
  label: string;
  onClick: () => void;
  solving: boolean;
  tech: string;
}

/**
 * A button component designed to handle optimization actions for a specific tech.
 */
const OptimizationButton: React.FC<OptimizationButtonProps> = ({
  label,
  onClick,
  solving,
  tech,
}) => {
  const hasTechInGrid = useGridStore((state) => state.hasTechInGrid(tech));
  const handleResetGridTech = useGridStore((state) => state.resetGridTech);
  const { max_bonus, clearTechMaxBonus } = useTechStore();

  const techMaxBonus = max_bonus?.[tech];

  const handleReset = () => {
    handleResetGridTech(tech);
    clearTechMaxBonus(tech);
  };

  return (
    <Flex className="items-center gap-2 mt-2 mb-2">
      {/* Optimization button */}
      <Tooltip content={hasTechInGrid ? "Update" : "Solve"}>
        <IconButton onClick={onClick} disabled={solving} variant="soft">
          {hasTechInGrid ? <UpdateIcon /> : <DoubleArrowLeftIcon />}
        </IconButton>
      </Tooltip>

      {/* Reset button: Explicit `else` case when `hasTechInGrid` is false */}
      {hasTechInGrid ? (
        <Tooltip content="Reset">
          <IconButton onClick={handleReset} disabled={solving} variant="soft">
            <ResetIcon />
          </IconButton>
        </Tooltip>
      ) : (
        <IconButton onClick={handleReset} disabled variant="soft">
          <ResetIcon />
        </IconButton>
      )}

      {/* Label */}
      <Text style={{ color: "var(--gray-12)" }}>{label}</Text>

      {/* Max bonus display */}
	  {techMaxBonus !== undefined && techMaxBonus !== 0 && (
        <Text
          className="font-thin font-condensed"
          style={{
            color: techMaxBonus > 101 ? "#e6c133" : "var(--gray-11)", // Highlight if > 101%
          }}
        >
          {techMaxBonus.toFixed(0)}%
        </Text>
      )}
    </Flex>
  );
};

export default OptimizationButton;
