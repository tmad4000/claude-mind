// Head-On Targeting Gun Module
// Fires directly at enemy's current position

protected void doGun() {
    if (getLastScanTime() == 0 || getGunHeat() > 0) {
        return;
    }

    // Calculate angle to enemy's current position
    double angleToEnemy = angleTo(getEnemyX(), getEnemyY());
    double gunTurn = Utils.normalRelativeAngle(angleToEnemy - getGunHeadingRadians());

    setTurnGunRightRadians(gunTurn);

    // Fire if gun is aimed
    if (Math.abs(gunTurn) < Math.toRadians(5)) {
        // Calculate fire power based on distance
        double firePower = calculateFirePower();
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
