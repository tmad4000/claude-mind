// Perpendicular Movement Module
// Moves perpendicular to the enemy, oscillating back and forth

private int moveDirection = 1;
private int perpDirection = 1;

protected void doMovement() {
    if (getLastScanTime() == 0) {
        // No enemy seen yet, just move forward
        setAhead(100);
        return;
    }

    // Calculate perpendicular angle to enemy
    double angleToEnemy = getHeadingRadians() + Math.toRadians(getEnemyBearing());
    double perpAngle = angleToEnemy + (Math.PI / 2) * perpDirection;

    // Desired distance from enemy
    double desiredDistance = PARAM_PREFERRED_DISTANCE;
    double distanceError = getEnemyDistance() - desiredDistance;

    // Adjust angle based on distance
    double adjustAngle = distanceError / 100.0; // Approach/retreat factor
    adjustAngle = Math.max(-0.5, Math.min(0.5, adjustAngle));
    double moveAngle = perpAngle + adjustAngle * perpDirection;

    // Set heading and move
    setTurnRightRadians(Utils.normalRelativeAngle(moveAngle - getHeadingRadians()));
    setAhead(PARAM_MOVE_DISTANCE * moveDirection);

    // Oscillate when close to walls or randomly
    if (Math.random() < PARAM_DIRECTION_CHANGE_RATE ||
        getX() < 50 || getX() > getBattleFieldWidth() - 50 ||
        getY() < 50 || getY() > getBattleFieldHeight() - 50) {
        moveDirection *= -1;
        if (Math.random() < 0.3) {
            perpDirection *= -1;
        }
    }
}
