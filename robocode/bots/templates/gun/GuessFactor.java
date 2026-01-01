// GuessFactor Targeting Gun Module
// Statistical targeting based on observed enemy movement patterns

private static final int GF_BINS = 31;
private static int[] gfStats = new int[GF_BINS];
private double lastFireTime = 0;

protected void doGun() {
    if (getLastScanTime() == 0 || getGunHeat() > 0) {
        return;
    }

    double firePower = calculateFirePower();
    double bulletSpeed = 20 - 3 * firePower;

    // Calculate max escape angle
    double maxEscapeAngle = Math.asin(8.0 / bulletSpeed);

    // Find the GuessFactor bin with highest hit rate
    int bestBin = GF_BINS / 2; // Default to center (head-on)
    int bestCount = 0;

    for (int i = 0; i < GF_BINS; i++) {
        if (gfStats[i] > bestCount) {
            bestCount = gfStats[i];
            bestBin = i;
        }
    }

    // Convert bin to GuessFactor (-1 to 1)
    double guessFactor = (bestBin - (GF_BINS - 1) / 2.0) / ((GF_BINS - 1) / 2.0);

    // Calculate firing angle
    double angleToEnemy = angleTo(getEnemyX(), getEnemyY());
    double fireAngle = angleToEnemy + guessFactor * maxEscapeAngle * getDirection();

    double gunTurn = Utils.normalRelativeAngle(fireAngle - getGunHeadingRadians());
    setTurnGunRightRadians(gunTurn);

    // Fire if gun is aimed
    if (Math.abs(gunTurn) < Math.toRadians(2)) {
        setFire(firePower);
        lastFireTime = getTime();
    }
}

private int getDirection() {
    // Determine if enemy is moving clockwise or counter-clockwise relative to us
    double angleToEnemy = angleTo(getEnemyX(), getEnemyY());
    double enemyHeadingRad = Math.toRadians(getEnemyHeading());
    double relativeBearing = Utils.normalRelativeAngle(enemyHeadingRad - angleToEnemy);

    return (relativeBearing * getEnemyVelocity() > 0) ? 1 : -1;
}

@Override
public void onBulletHit(BulletHitEvent e) {
    // Update GuessFactor statistics
    updateGFStats(e.getBullet(), true);
}

@Override
public void onBulletMissed(BulletMissedEvent e) {
    // Could track misses for negative learning
}

private void updateGFStats(Bullet bullet, boolean hit) {
    // Simple: just increment the center bin on hit
    // Real implementation would track the actual GF that hit
    if (hit) {
        int bin = GF_BINS / 2;
        // Adjust based on enemy velocity at time of fire
        bin += (int)(getEnemyVelocity() * getDirection() * (GF_BINS / 16.0));
        bin = Math.max(0, Math.min(GF_BINS - 1, bin));
        gfStats[bin]++;
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
