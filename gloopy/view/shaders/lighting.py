from ..shader import Shader

VERTEX = """
attribute vec3 position;
attribute vec4 color;
attribute vec3 normal;

varying vec4 baseColor;

void main()
{
    vec4 ambientColor = vec4(0.325, 0.150, 0.007, 1.0);
    vec3 lightDir = vec3(0.267, 0.267 * 3.0, 0.267 * 2.0);
    vec4 lightColor = vec4(1.0, 1.0, 1.0, 1.0);

    gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);

    float nDotL = dot(normal, lightDir);
 
    // fake lighting of backfaces too
    // perhaps remove this when we have more than one lightsource
    nDotL = 0.5 + nDotL * 0.5;

    nDotL = max(nDotL, 0.0);
    vec4 diffuse_weight = color * lightColor;

    baseColor = (
        ambientColor * color +
        nDotL * diffuse_weight
    );
}
"""
FRAGMENT = """
varying vec4 baseColor;

out vec4 fragColor;

void main()
{
    fragColor = baseColor;
}
"""

lighting = Shader(VERTEX, FRAGMENT, ['position', 'color', 'normal'])

