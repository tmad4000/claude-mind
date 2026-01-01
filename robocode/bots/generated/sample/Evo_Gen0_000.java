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
public class Evo_Gen0_000 extends AdvancedRobot {

    // === PARAMETERS (injected during generation) ===
        private static final double PARAM_PREFERRED_DISTANCE = 344.0774;
    private static final double PARAM_MOVE_DISTANCE = 64.1798;
    private static final double PARAM_DIRECTION_CHANGE_RATE = 0.0426;
    private static final double PARAM_DIRECTION_CHANGE_INTERVAL = 40.4563;
    private static final double PARAM_RANDOM_CHANGE_RATE = 0.0203;
    private static final double PARAM_MAX_TURN_ANGLE = 68.9110;
    private static final double PARAM_FIRE_POWER_CLOSE = 2.7526;
    private static final double PARAM_FIRE_POWER_MEDIUM = 1.7374;
    private static final double PARAM_FIRE_POWER_FAR = 0.6045;
    private static final double PARAM_RADAR_LOCK_EXTRA = 16.9361;

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
        setColors(Color.decode("#FF00FF"),
                  Color.decode("#80FF00"),
                  Color.decode("#00FFFF"));

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
    // Basic Wave Surfer Movement Module
// Attempts to dodge bullets by tracking enemy energy drops

import java.util.ArrayList;

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


    // === GUN MODULE ===
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
