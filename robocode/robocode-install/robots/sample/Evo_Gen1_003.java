package sample;

import robocode.*;
import robocode.util.Utils;
import java.awt.Color;
import java.awt.geom.Point2D;
import java.util.ArrayList;

/**
 * BaseAdvancedBot - Template for evolved bots
 *
 * This bot uses a modular architecture:
 * - Movement: Handles how the robot moves
 * - Gun: Handles targeting and firing
 * - Radar: Handles enemy detection
 *
 * Parameters are injected during generation.
 */
public class Evo_Gen1_003 extends AdvancedRobot {

    // === PARAMETERS (injected during generation) ===
        private static final double PARAM_PREFERRED_DISTANCE = 379.5182;
    private static final double PARAM_MOVE_DISTANCE = 172.2213;
    private static final double PARAM_DIRECTION_CHANGE_RATE = 0.0380;
    private static final double PARAM_DIRECTION_CHANGE_INTERVAL = 25.0386;
    private static final double PARAM_RANDOM_CHANGE_RATE = 0.0298;
    private static final double PARAM_MAX_TURN_ANGLE = 75.1676;
    private static final double PARAM_FIRE_POWER_CLOSE = 2.7521;
    private static final double PARAM_FIRE_POWER_MEDIUM = 1.7983;
    private static final double PARAM_FIRE_POWER_FAR = 0.9479;
    private static final double PARAM_RADAR_LOCK_EXTRA = 15.5359;

    // === STATE ===
    private double enemyX, enemyY;
    private double enemyHeading, enemyVelocity;
    private double enemyBearing, enemyDistance;
    private double enemyEnergy = 100;
    private long lastScanTime = 0;

    // Gun heat tracking
    private double lastEnemyEnergy = 100;

    /**
     * Main robot loop
     */
    public void run() {
        // Set colors
        setColors(Color.decode("#FFFF00"),
                  Color.decode("#FF8000"),
                  Color.decode("#FF00FF"));

        // Independent movement
        setAdjustGunForRobotTurn(true);
        setAdjustRadarForGunTurn(true);

        // Main loop
        while (true) {
            doRadar();
            doMovement();
            doGun();
            execute();
        }
    }

    /**
     * Called when we scan a robot
     */
    public void onScannedRobot(ScannedRobotEvent e) {
        lastScanTime = getTime();

        // Update enemy state
        enemyBearing = e.getBearing();
        enemyDistance = e.getDistance();
        enemyHeading = e.getHeading();
        enemyVelocity = e.getVelocity();

        // Calculate absolute position
        double angle = Math.toRadians(getHeading() + enemyBearing);
        enemyX = getX() + enemyDistance * Math.sin(angle);
        enemyY = getY() + enemyDistance * Math.cos(angle);

        // Detect enemy firing (energy drop)
        double energyDrop = lastEnemyEnergy - e.getEnergy();
        if (energyDrop > 0 && energyDrop <= 3) {
            onEnemyFired(energyDrop);
        }
        lastEnemyEnergy = e.getEnergy();
    }

    /**
     * Called when enemy fires (detected via energy drop)
     */
    protected void onEnemyFired(double bulletPower) {
        // Override in movement module for wave surfing
    }

    // === RADAR MODULE ===
    // Spin Radar Module
// Continuous radar sweep to detect all enemies

protected void doRadar() {
    // Always spin radar
    setTurnRadarRight(360);
}


    // === MOVEMENT MODULE ===
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


    // === GUN MODULE ===
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


    // === UTILITY METHODS ===

    protected double getEnemyX() { return enemyX; }
    protected double getEnemyY() { return enemyY; }
    protected double getEnemyHeading() { return enemyHeading; }
    protected double getEnemyVelocity() { return enemyVelocity; }
    protected double getEnemyBearing() { return enemyBearing; }
    protected double getEnemyDistance() { return enemyDistance; }
    protected long getLastScanTime() { return lastScanTime; }

    /**
     * Calculate angle to a point
     */
    protected double angleTo(double x, double y) {
        return Math.atan2(x - getX(), y - getY());
    }

    /**
     * Normalize angle to -PI to PI
     */
    protected double normalizeAngle(double angle) {
        return Utils.normalRelativeAngle(angle);
    }
}
