from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Listing, Image
from .forms import ImageForm
from .forms import ListingForm


@login_required
def listing_list(request):
    listings = Listing.objects.filter(member__user=request.user).order_by('-created_at')
    context = {
        'listings': listings
    }
    return render(request, 'listings/listing_list.html', context)


@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.member = request.user.member
            listing.save()
            return redirect('listing_list')
    else:
        form = ListingForm()
    return render(request, 'listings/listing_create.html', {'form': form})


@login_required
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk, member=request.user.member)
    images = Image.objects.filter(listing=listing)  # Retrieve all images for the listing
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_list')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/listing_update.html', {
        'form': form,
        'listing': listing,
        'images': images  # Pass the images to the template
    })


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, member=request.user.member)
    if request.method == 'POST':
        listing.delete()
        return redirect('listing_list')
    return render(request, 'listings/listing_confirm_delete.html', {'listing': listing})


@login_required
def image_list(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk, member=request.user.member)
    images = listing.images.all()
    return render(request, 'images/image_list.html', {'listing': listing, 'images': images})


@login_required
def image_create(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk, member=request.user.member)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.listing = listing
            image.save()
            return redirect('image_list', listing_pk=listing.pk)
    else:
        form = ImageForm()
    return render(request, 'images/image_form.html', {'form': form, 'listing': listing})


@login_required
def image_delete(request, listing_pk, image_pk):
    listing = get_object_or_404(Listing, pk=listing_pk, member=request.user.member)
    image = get_object_or_404(Image, pk=image_pk, listing=listing)

    if request.method == 'POST':
        # Delete the image file from S3
        image.image.delete(save=False)
        # Delete the image object from the database
        image.delete()
        return redirect('image_list', listing_pk=listing.pk)

    return render(request, 'images/image_confirm_delete.html', {'listing': listing, 'image': image})
