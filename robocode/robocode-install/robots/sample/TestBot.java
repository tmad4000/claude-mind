package sample;

import robocode.*;
import robocode.util.Utils;
import java.awt.Color;
import java.awt.geom.Point2D;

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
public class TestBot extends AdvancedRobot {

    // === PARAMETERS (injected during generation) ===
        private static final double PARAM_PREFERRED_DISTANCE = 217.0810;
    private static final double PARAM_MOVE_DISTANCE = 199.6879;
    private static final double PARAM_DIRECTION_CHANGE_RATE = 0.0101;
    private static final double PARAM_DIRECTION_CHANGE_INTERVAL = 12.6406;
    private static final double PARAM_RANDOM_CHANGE_RATE = 0.0445;
    private static final double PARAM_MAX_TURN_ANGLE = 57.5998;
    private static final double PARAM_FIRE_POWER_CLOSE = 2.9217;
    private static final double PARAM_FIRE_POWER_MEDIUM = 1.8255;
    private static final double PARAM_FIRE_POWER_FAR = 1.0432;
    private static final double PARAM_RADAR_LOCK_EXTRA = 14.7849;

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
        setColors(Color.decode("#8000FF"),
                  Color.decode("#800000"),
                  Color.decode("#008000"));

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
    // Lock Radar Module
// Locks onto enemy for continuous tracking (1v1 optimal)

protected void doRadar() {
    if (getLastScanTime() == 0) {
        // No enemy seen yet, spin to find one
        setTurnRadarRight(360);
        return;
    }

    // Calculate angle to enemy
    double angleToEnemy = getHeadingRadians() + Math.toRadians(getEnemyBearing());
    double radarTurn = Utils.normalRelativeAngle(angleToEnemy - getRadarHeadingRadians());

    // Add extra turn to ensure we keep scanning (oscillate)
    double extraTurn = Math.signum(radarTurn) * Math.toRadians(PARAM_RADAR_LOCK_EXTRA);

    setTurnRadarRightRadians(radarTurn + extraTurn);
}


    // === MOVEMENT MODULE ===
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


    // === GUN MODULE ===
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
