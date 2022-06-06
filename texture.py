from dataclasses import dataclass


@dataclass
class TextureTypeInfo:
    name: str
    bytes_per_block: int
    px_block_dimension: int


texture_types = {
    77: TextureTypeInfo('bc7', 16, 4),
}


# copied from PredatorCZ/XenoLib
# https://github.com/PredatorCZ/XenoLib/blob/2f14c0bd3765ee4439e91034028c0acb0493f95f/source/LBIM.cpp#L204
# GPLv3 License https://www.gnu.org/licenses/
def get_swizzled_offset(x: int, y: int, w: int, bytes_per_block: int, x_bits_shift: int):
    x *= bytes_per_block
    return ((y & 0xff80) * w * bytes_per_block) | ((y & 0x78) << 6) | ((y & 6) << 5) | ((y & 1) << 4) \
           | ((x & 0xffc0) << x_bits_shift) | ((x & 0x20) << 3) | ((x & 0x10) << 1) | (x & 0xf)


def get_swizzle_bits_shift(h: int):
    x_bits_shift = 3
    for i in range(4):
        if (h - 1) & (8 << i):
            x_bits_shift += 1
    return x_bits_shift


def get_swizzled_texture(texture_data: bytes, texture_type: int, w: int, h: int):
    texture_type_info = texture_types[texture_type]
    bytes_per_block = texture_type_info.bytes_per_block
    px_block_dimension = texture_type_info.px_block_dimension
    blocks_w = w // px_block_dimension
    blocks_h = h // px_block_dimension
    x_bits_shift = get_swizzle_bits_shift(blocks_h)

    swizzled = bytearray(len(texture_data))
    current_offset = 0
    for y in range(blocks_h):
        for x in range(blocks_w):
            swizzled_offset = get_swizzled_offset(x, y, blocks_w, bytes_per_block, x_bits_shift)
            swizzled[swizzled_offset:swizzled_offset + bytes_per_block] \
                = texture_data[current_offset:current_offset + bytes_per_block]
            current_offset += bytes_per_block

    return swizzled
