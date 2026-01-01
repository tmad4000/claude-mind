// Linear Targeting Gun Module
// Predicts enemy position assuming constant velocity

protected void doGun() {
    if (getLastScanTime() == 0 || getGunHeat() > 0) {
        return;
    }

    // Calculate fire power first (affects bullet speed)
    double firePower = calculateFirePower();
    double bulletSpeed = 20 - 3 * firePower;

    // Time for bullet to reach enemy
    double distance = getEnemyDistance();
    double bulletTime = distance / bulletSpeed;

    // Predict enemy position
    double enemyHeadingRad = Math.toRadians(getEnemyHeading());
    double predictedX = getEnemyX() + getEnemyVelocity() * Math.sin(enemyHeadingRad) * bulletTime;
    double predictedY = getEnemyY() + getEnemyVelocity() * Math.cos(enemyHeadingRad) * bulletTime;

    // Clamp to battlefield
    predictedX = Math.max(18, Math.min(getBattleFieldWidth() - 18, predictedX));
    predictedY = Math.max(18, Math.min(getBattleFieldHeight() - 18, predictedY));

    // Calculate angle to predicted position
    double angleToTarget = angleTo(predictedX, predictedY);
    double gunTurn = Utils.normalRelativeAngle(angleToTarget - getGunHeadingRadians());

    setTurnGunRightRadians(gunTurn);

    // Fire if gun is aimed
    if (Math.abs(gunTurn) < Math.toRadians(3)) {
        setFire(firePower);
    }
}

private double calculateFirePower() {
    double distance = getEnemyDistance();

    if (distance < 150) {
        return PARAM_FIRE_POWER_CLOSE;
    } else if (distance < 400) {
        return PARAM_FIRE_POWER_MEDIUM;
    } else {
        return PARAM_FIRE_POWER_FAR;
    }
}
