
attribute vec3 position;
attribute vec4 color;
attribute vec3 normal;

varying vec4 baseColor;

// both parameters must be normalised
float dLight( 
    in vec3 light_dir, 
    in vec3 surface_norm
) {
    float value = dot(surface_norm, light_dir);
    // cheat to make effects of directional light extend across the dark side
    // of objects. Hopefully this will be less necessary when more than one
    // lightsource is in the scene.
    value = 0.5 + value * 0.5;
    return max(0.0, value);
}

// ambient light color:
//uniform vec4 global_ambient;

// light source direction
//uniform vec3 Light_direction;

// light's color:
//uniform vec4 light_color;

// light_ambient is a bit pointless. I'm content to assume a lightsource
// doesn't contribute to the ambient light level
//uniform vec4 Light_ambient;

// presumably it usually makes perfect sense to use the same value - namely
// color - for both of these, since a material's scattering of incoming light
// is identical regardless of whether that light is from a directional source,
// or ambient
//uniform vec4 Material_ambient;
//uniform vec4 material_diffuse;

void main()
{
    vec3 light_dir = vec3(0.2670, 0.267 * 3.0, 0.2673 * -2.0);
    vec4 global_ambient= vec4(0.1, 0.1, 0.1, 1.0);
    vec4 light_color = vec4(1.0, 1.0, 1.0, 1.0);
    vec4 material_diffuse = vec4(1.0, 1.0, 1.0, 1.0);

    gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
    float diffuse_weight = dLight(
        normalize(gl_NormalMatrix * light_dir),
        normalize(gl_NormalMatrix * normal)
    );
    
    baseColor = (
        global_ambient * color
        + color * light_color * diffuse_weight
        // + color * Light_ambient
    );
}

