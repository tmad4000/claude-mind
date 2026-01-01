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
