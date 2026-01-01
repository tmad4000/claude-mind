// Random Movement Module
// Unpredictable movement with direction changes

private int randomMoveDirection = 1;
private double randomTurnAmount = 0;
private long lastDirectionChange = 0;

protected void doMovement() {
    long timeSinceChange = getTime() - lastDirectionChange;

    // Change direction periodically or when hitting walls
    boolean shouldChange = timeSinceChange > PARAM_DIRECTION_CHANGE_INTERVAL ||
        Math.random() < PARAM_RANDOM_CHANGE_RATE ||
        getX() < 40 || getX() > getBattleFieldWidth() - 40 ||
        getY() < 40 || getY() > getBattleFieldHeight() - 40;

    if (shouldChange) {
        randomMoveDirection = Math.random() < 0.5 ? 1 : -1;
        randomTurnAmount = (Math.random() - 0.5) * PARAM_MAX_TURN_ANGLE;
        lastDirectionChange = getTime();
    }

    // Apply movement
    setTurnRight(randomTurnAmount);
    setAhead(PARAM_MOVE_DISTANCE * randomMoveDirection);

    // If we have an enemy, slightly bias toward perpendicular
    if (getLastScanTime() > 0 && Math.random() < 0.3) {
        double perpAngle = getEnemyBearing() + 90 * randomMoveDirection;
        setTurnRight(Utils.normalRelativeAngleDegrees(perpAngle - getHeading()) * 0.1);
    }
}
