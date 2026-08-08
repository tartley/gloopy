from ..shader import Shader

_VERTEX = """
#version 120

attribute vec3 position;
attribute vec4 color;
attribute vec3 normal;

varying vec4 baseColor;

void main()
{
    vec4 ambientLightColor = vec4(0.325, 0.150, 0.007, 1.0);
    vec3 dirLightDir = vec3(0.267, 0.267 * 3.0, 0.267 * 2.0);
    vec4 dirLightColor = vec4(1.0, 1.0, 1.0, 1.0);

    gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
    
    float nDotL = dot(gl_NormalMatrix * normal, dirLightDir);
 
    // fake lighting of backfaces too
    // perhaps remove this when we have more than one lightsource
    nDotL = 0.5 + nDotL * 0.5;

    nDotL = max(nDotL, 0.0);
    vec4 diffuse_weight = color * dirLightColor;

    baseColor = (
        ambientLightColor * color +
        nDotL * diffuse_weight
    );
}
"""
_FRAGMENT = """
#version 120

varying vec4 baseColor;

void main()
{
    gl_FragColor = baseColor;
}
"""

lighting = Shader(_VERTEX, _FRAGMENT, ['position', 'color', 'normal'])

