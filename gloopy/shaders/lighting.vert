
attribute vec3 position;
attribute vec4 color;
attribute vec3 normal;

varying vec4 baseColor;

// The correct dLight implementation.
// Faces at greater than 90deg to the light source (i.e. facing away from it)
// do not receive any illumination.
// Both parameters must be normalised
float dLight( 
    in vec3 lightDir, 
    in vec3 surface_norm
) {
    return max(0.0, dot(surface_norm, lightDir));
}

// An alternative dLight implementation.
// Faces at greater than 90deg to the light source still receive diminishing
// illumination from it. This is useful to prevent all dark faces from
// becoming a single large field of homogoneous darkness. Hopefully this will
// be less necessary when more then one lightsource is present.
// Both parameters must be normalised
float dLight_cheat( 
    in vec3 lightDir, 
    in vec3 surface_norm
) {
    return 0.5 + dot(surface_norm, lightDir) * 0.5;
}

void main()
{
    // 1/sqrt(14) == 0.267
    vec4 ambientColor = vec4(0.1, 0.1, 0.1, 1.0);
    vec3 lightDir = vec3(0.267, 0.267 * 3.0, 0.267 * -2.0);
    vec4 lightColor = vec4(1.0, 1.0, 1.0, 1.0);

    gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);

    float diffuse_weight = dLight_cheat(
        normalize(gl_NormalMatrix * lightDir),
        normalize(gl_NormalMatrix * normal)
    );
    baseColor = (
        ambientColor * color
        + color * lightColor * diffuse_weight
    );
}

