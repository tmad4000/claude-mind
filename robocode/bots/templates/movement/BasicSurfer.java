// Basic Wave Surfer Movement Module
// Attempts to dodge bullets by tracking enemy energy drops

private ArrayList<Double> waves = new ArrayList<>();
private int surfDirection = 1;

protected void doMovement() {
    if (getLastScanTime() == 0) {
        setAhead(100);
        return;
    }

    // Update waves (bullets travel toward us)
    updateWaves();

    // If no active waves, just do perpendicular movement
    if (waves.isEmpty()) {
        doPerpMovement();
        return;
    }

    // Find safest direction
    double clockwiseDanger = checkDanger(1);
    double counterDanger = checkDanger(-1);

    // Choose safer direction
    if (clockwiseDanger < counterDanger) {
        surfDirection = 1;
    } else if (counterDanger < clockwiseDanger) {
        surfDirection = -1;
    }
    // Otherwise keep current direction

    // Move perpendicular to enemy
    doPerpMovement();
}

private void doPerpMovement() {
    double angleToEnemy = getHeadingRadians() + Math.toRadians(getEnemyBearing());
    double perpAngle = angleToEnemy + (Math.PI / 2) * surfDirection;

    setTurnRightRadians(Utils.normalRelativeAngle(perpAngle - getHeadingRadians()));
    setAhead(PARAM_MOVE_DISTANCE * surfDirection);

    // Wall smoothing
    if (getX() < 50 || getX() > getBattleFieldWidth() - 50 ||
        getY() < 50 || getY() > getBattleFieldHeight() - 50) {
        surfDirection *= -1;
    }
}

@Override
protected void onEnemyFired(double bulletPower) {
    // Add a wave (simplified - just tracks that a bullet was fired)
    double bulletSpeed = 20 - 3 * bulletPower;
    waves.add(bulletSpeed);

    // Limit wave tracking
    if (waves.size() > 10) {
        waves.remove(0);
    }
}

private void updateWaves() {
    // Simple wave aging - remove old waves
    if (!waves.isEmpty() && Math.random() < 0.1) {
        waves.remove(0);
    }
}

private double checkDanger(int direction) {
    // Simplified danger calculation
    // Real wave surfing would predict bullet positions
    // This just estimates based on wave count and direction
    double danger = waves.size() * 0.1;

    // Add wall danger
    double futureX = getX() + Math.sin(getHeadingRadians()) * 100 * direction;
    double futureY = getY() + Math.cos(getHeadingRadians()) * 100 * direction;

    if (futureX < 30 || futureX > getBattleFieldWidth() - 30) danger += 0.5;
    if (futureY < 30 || futureY > getBattleFieldHeight() - 30) danger += 0.5;

    return danger;
}
