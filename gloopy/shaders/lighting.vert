
attribute vec3 position;
attribute vec4 color;
attribute vec3 normal;

varying vec4 baseColor;

// both parameters must be normalised
float dLight( 
    in vec3 light_pos, 
    in vec3 surface_norm
) {
    float value = dot(surface_norm, light_pos);
    // cheat to make directional light extend right across dark side of objects
    value = 0.5 + value * 0.5;
    return value;
    //return max(0.0, value);
}

//uniform vec4 Global_ambient;
//uniform vec4 Light_ambient;
//uniform vec4 Light_diffuse;
//uniform vec3 Light_location;
//uniform vec4 Material_ambient;
//uniform vec4 Material_diffuse;

void main()
{
    vec3 light_pos = vec3(0.2670, 0.267 * 3.0, 0.2673 * -2.0);
    vec4 Global_ambient= vec4(0.1, 0.1, 0.1, 1.0);
    vec4 Light_diffuse = vec4(1.0, 1.0, 1.0, 1.0);
    vec4 Material_diffuse = vec4(1.0, 1.0, 1.0, 1.0);

    gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
    float diffuse_weight = dLight(
        normalize(gl_NormalMatrix * light_pos),
        normalize(gl_NormalMatrix * normal)
    );
    
    // Light_ambient * Material_ambient +
    baseColor = (
        Global_ambient * color +
        color * Light_diffuse * diffuse_weight
    );
}

